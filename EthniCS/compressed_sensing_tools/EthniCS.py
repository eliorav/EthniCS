import numpy as np
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio
from .services.get_sparseness import get_sparseness
from .services.fine_tune_result import fine_tuning_result
from .EthniCS_config import EthniCSConfig


class EthniCS:
    def __init__(self, ethnics_config:EthniCSConfig):
        """
        Initializes an instance of the EthniCS class.

        Parameters:
        - ethnics_config (EthniCSConfig): The configuration object for EthniCS.
        """
        self.ethnics_config = ethnics_config

    def solve(self, phi, y, solvers_data, similar_solvers=[]):
        """
        Returns the best solution from a list of solvers results for the CS problem.

        Parameters:
        - phi: The measurement matrix.
        - y: The observed signal.
        - solvers_data: A dictionary containing the results of different solvers.
        - similar_solvers: A list of tuples representing similar solvers.

        Returns:
        - The best solution for the CS problem.
        - The confidence of the best solution.
        """
        best_solver, confidence = self.get_best_solver(phi, y, solvers_data, similar_solvers)
        x_res, a_hat, _ = solvers_data[best_solver['name']]
        is_sparse = get_sparseness(a_hat) > int(phi.shape[1] * self.ethnics_config.sparseness_threshold)

        return (
            fine_tuning_result(phi, x_res, y, max_iter=self.ethnics_config.fine_tune_max_iter)
            if is_sparse
            else x_res,
            confidence,
        )
    
    def get_best_solver(self, phi, y, solvers_data, similar_solvers):
        """
        Returns the best solver and its confidence based on the given solvers data.

        Parameters:
        - phi: The measurement matrix.
        - y: The observed signal.
        - solvers_data: A dictionary containing the results of different solvers.
        - similar_solvers: A list of tuples representing similar solvers.

        Returns:
        - The best solver.
        - The confidence of the best solver.
        """
        similar_solvers = self.get_similar_solutions(solvers_data, similar_solvers)
        solvers_stats = self.get_solvers_stats(y, solvers_data)

        solvers_with_support = similar_solvers.first_sol.unique().tolist() 
        selected_solvers = solvers_stats.set_index('name')

        confidence = 1

        if len(solvers_with_support) > 0:
            strong_solvers = selected_solvers[selected_solvers.psnr > self.ethnics_config.high_psnr_threshold].reset_index().name.to_list()
            selected_solvers = selected_solvers.loc[solvers_with_support+strong_solvers].sort_values('score', ascending=False)
        else:
            confidence *= 0.8

        if selected_solvers[selected_solvers.psnr > self.ethnics_config.medium_psnr_threshold].shape[0] > 0:
            selected_solvers = selected_solvers[selected_solvers.psnr > self.ethnics_config.medium_psnr_threshold].sort_values('score', ascending=False)

        best_solver = selected_solvers.reset_index().iloc[0].to_dict()
        confidence *= self.get_confidence_by_stats(phi, best_solver['psnr'], best_solver['sparseness'])

        return best_solver, confidence
    
    def get_solvers_stats(self, y, solvers_data):
        """
        Returns the statistics of the solvers based on the given solvers data.

        Parameters:
        - y: The observed signal.
        - solvers_data: A dictionary containing the results of different solvers.

        Returns:
        - A DataFrame containing the statistics of the solvers.
        """
        res = []
        n = y.shape[0]

        for sol_name, sol_data in solvers_data.items():
            _, a_hat, y_hat = sol_data
            signal_sparseness = get_sparseness(a_hat)
            psnr_score = peak_signal_noise_ratio(y, y_hat, data_range=1)
            
            # SR measures the fraction of zero elements in the signal
            sr = signal_sparseness/n

            # The score is the sparseness of the signal and the fittest to y (using PSNR score)
            score = sr + (self.ethnics_config.alpha/n) * psnr_score
            res += [dict(name=sol_name, psnr=psnr_score, sparseness=signal_sparseness, score=score)]

        return pd.DataFrame(res).sort_values('score', ascending=False)


    def get_similar_solutions(self, solvers_data, similar_solvers):
        """
        Returns the similar solutions based on the given solvers data and similar solvers list.

        Parameters:
        - solvers_data: A dictionary containing the results of different solvers.
        - similar_solvers: A list of tuples representing similar solvers.

        Returns:
        - A DataFrame containing the similar solutions.
        """
        res = []
        solvers = list(solvers_data.items())
        
        for first_sol_name, first_sol_data in solvers:
            for sec_sol_name, sec_sol_data in solvers:
                should_skip = False
                
                for s_name1, s_name2 in similar_solvers:
                    if first_sol_name[1] == s_name1 and sec_sol_name[1] == s_name2 or first_sol_name[1] == s_name2 and sec_sol_name[1] == s_name1:
                        should_skip = True
                        continue

                if should_skip:
                    continue
                if first_sol_name[1] == sec_sol_name[1] or first_sol_name == sec_sol_name:
                    continue

                res += [dict(first_sol=first_sol_name, sec_sol=sec_sol_name, psnr=peak_signal_noise_ratio(first_sol_data[0], sec_sol_data[0], data_range=1))]

        df = pd.DataFrame(res)
        return df[df.psnr > self.ethnics_config.low_psnr_threshold].sort_values('psnr', ascending=False)


    def get_confidence_by_stats(self, phi, psnr, sparseness):
        """
        Returns the confidence based on the given statistics.

        Parameters:
        - phi: The measurement matrix.
        - psnr: The PSNR score.
        - sparseness: The sparseness of the signal.

        Returns:
        - The confidence.
        """
        confidence = 1
        sparseness_ratio = sparseness/phi.shape[1]

        if psnr > self.ethnics_config.perfect_psnr_threshold and sparseness_ratio > self.ethnics_config.sparseness_threshold:
            return 1

        if  self.ethnics_config.high_psnr_threshold <= psnr < self.ethnics_config.perfect_psnr_threshold:
            if sparseness_ratio < self.ethnics_config.sparseness_threshold:
                confidence *= 0.9 * min(psnr/self.ethnics_config.perfect_psnr_threshold, 0.7)
        elif self.ethnics_config.low_psnr_threshold <= psnr < self.ethnics_config.high_psnr_threshold:
            confidence *= 0.6 * min(psnr/self.ethnics_config.high_psnr_threshold, 0.5)
        else:
            confidence *= 0.4 * min(psnr/self.ethnics_config.low_psnr_threshold, 0.5)

        if 0.5 < sparseness_ratio <= self.ethnics_config.sparseness_threshold:
            confidence *= 0.7
        elif sparseness_ratio <= 0.5:
            confidence *= 0.5

        return confidence