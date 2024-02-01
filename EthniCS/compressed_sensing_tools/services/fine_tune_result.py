import torch
from .get_sensing_vector import get_sensing_vector


def fine_tuning_result(phi, x_init, y, max_iter=10000, lr=1e-5):
    """
    Minimize the loss between y_hat and phi@x_hat by changing x_hat using Adam optimizer
    """

    def update(x, phi, y, optimizer, criterion):
        y_hat = get_sensing_vector(phi, x)
        loss = criterion(y, y_hat)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        with torch.no_grad():
            x.clamp_(0, 1)
        return loss.item()

    criterion = torch.nn.MSELoss()
    phi = torch.tensor(phi)
    x = torch.tensor(x_init, requires_grad=True)
    y = torch.tensor(y)
    optimizer = torch.optim.Adam([x], lr=lr)

    min_loss = 100000
    min_x = None

    for _ in range(max_iter):
        loss = update(x, phi, y, optimizer, criterion)

        if loss < min_loss:
            min_loss = loss
            min_x = x.detach().numpy()

    return min_x
