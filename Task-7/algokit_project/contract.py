from algopy import ARC4Contract
from smart_contracts.approval_program import approval_program
from smart_contracts.clear_program import clear_state_program

class NFTMarketplaceContract(ARC4Contract):
    def approval_program(self):
        return approval_program(self.creator)

    def clear_state_program(self):
        return clear_state_program()