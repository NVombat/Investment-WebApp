import torch
from tqdm import tqdm


class Trainer:
    def __init__(self, model: torch.nn.Module, optimizer: torch.optim,
                 criterion: torch.nn.CrossEntropyLoss):

        self.model = model
        self.optim = optimizer
        self.device = torch.device('cuda') if torch.cuda.is_available() else 'cpu'
        self.criterion = criterion
        self.model = model.to(self.device)


    def train(self, train_loader) -> tuple:
        """
        :param model:
        :param optim:
        :param dl:
        :return epoch_loss, epoch_acc:
        """
        self.model.train()
        epoch_loss = 0

        for xid, (feature, label) in tqdm(enumerate(train_loader), total=len(train_loader)):
            self.optim.zero_grad()
            feature, label = feature.to(self.device), label.to(self.device)
            out = self.model(feature)
            loss = self.criterion(out, label)

            loss.backward()

            self.optim.step()

            epoch_loss += loss.item()

        return epoch_loss / len(train_loader)

    def test(self, test_loader) -> torch.tensor:
        """
        :param model:
        :param test_dl:
        :return test_accuracy:
        """
        self.model.eval()
        for xid, (feature, label) in tqdm(enumerate(test_loader), total=len(test_loader)):
            with torch.no_grad():
                feature = feature.to(self.device)

        # TODO : ADD RMSE

