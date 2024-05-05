from block import Block
import datetime as dt
from key import generate_keys

class Blockchain:
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.chain = [self.create_first_block()]

    def create_first_block(self):
        return Block(0, "First block", dt.datetime.now(), "0", self.public_key)
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, new_block):
        new_block.previous_key = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        new_block.sign_block(self.private_key)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_key != previous_block.hash:
                return False
        return True
    def get_blocks(self):
        for block in self.chain:
            print("Block #", block.index)
            print("Data: ", block.data)
            print("Time: ", block.time)
            print("Previous Hash: ", block.previous_key)
            print("Hash: ", block.hash)
            print("\n")
    def find_block_by_private_key(self, private_key):
        for block in self.chain:
            print("Block private key: ", block.private_key)
            print("\nPassed inPrivate key: ", private_key)
            if block.private_key == private_key:
                print("I found the block!!")
                return block
        return None

        
    
    
generated_public_key, generated_private_key = generate_keys()
blockchain = Blockchain(generated_public_key, generated_private_key)

# blockchain.add_block(Block(1, "Biden", dt.datetime.now(), blockchain.get_latest_block().hash, generated_public_key, generated_private_key))
# blockchain.add_block(Block(2, "Trump", dt.datetime.now(), blockchain.get_latest_block().hash, generated_public_key, generated_private_key))
# blockchain.add_block(Block(3, "Trump", dt.datetime.now(), blockchain.get_latest_block().hash, generated_public_key, generated_private_key))
# blockchain.add_block(Block(4, "RFK JR", dt.datetime.now(), blockchain.get_latest_block().hash, generated_public_key, generated_private_key))

# for block in blockchain.chain:
#     print("Block #", block.index)
#     print("Data: ", block.data)
#     print("Time: ", block.time)
#     print("Previous Hash: ", block.previous_key)
#     print("Hash: ", block.hash)
#     print("\n")

