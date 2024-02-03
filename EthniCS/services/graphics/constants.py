from ...constants import ETHNICS_SOLVER

supported_solvers = {
    'CoSaMP - identity': 2,
    'FISTA - identity': 3,
    'GPSR-BB - DWT': 4,
    'GPSR-BB - identity': 5,
    'ISTA - DWT': 6,
    'OMP - identity': 7,
    'SCS - DWT': 8,
    'SCS - identity': 9,
    'all zeros': 10,
    ETHNICS_SOLVER: 11,
}

solver_to_color = {'OMP - identity': '#AA0DFE', 'OMP - DCT': '#3283FE', 'OMP - DWT': '#85660D', 'CoSaMP - identity': '#782AB6', 'CoSaMP - DCT': '#565656', 'CoSaMP - DWT': '#1C8356', 'FISTA - identity': '#16FF32', 'FISTA - DCT': '#F7E1A0', 'FISTA - DWT': '#E2E2E2', 'GPSR-BB - identity': '#1CBE4F', 'GPSR-BB - DCT': '#C4451C', 'GPSR-BB - DWT': '#DEA0FD', 'SCS - identity': '#FE00FA', 'SCS - DCT': '#325A9B', 'SCS - DWT': '#FEAF16', 'ISTA - identity': '#F8A19F', 'ISTA - DCT': '#90AD1C', 'ISTA - DWT': '#F6222E', ETHNICS_SOLVER: '#1CFFCE', 'all zeros': '#2ED9FF'}
