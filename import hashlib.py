import tkinter as tk
import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.latest_block = None  # Store the latest block

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        global block
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        self.latest_block = block  # Update the latest block
        return block

    def new_transaction(self, voter_id, candidate):
        self.current_transactions.append({
            'voter_id': voter_id,
            'candidate': candidate,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

class VotingApp:
    # global current_transactions
    def __init__(self, master, blockchain):
        self.master = master
        self.master.title("Voting App")
        self.blockchain = blockchain

        self.blue_button = tk.Button(self.master, text="Blue", bg="blue", command=self.vote_blue)
        self.blue_button.pack()

        self.red_button = tk.Button(self.master, text="Red", bg="red", command=self.vote_red)
        self.red_button.pack()

        self.display_votes()

    def vote_blue(self):
        self.blockchain.new_transaction("voter1", "Blue")
        print("Voted for Blue")
        self.display_votes()

    def vote_red(self):
        self.blockchain.new_transaction("voter1", "Red")
        print("Voted for Red")
        self.display_votes()

    def display_votes(self):
        for widget in self.master.winfo_children():
            if widget not in [self.blue_button, self.red_button]:
                widget.destroy()

        if self.blockchain.latest_block:
            votes = [transaction['candidate'] for transaction in self.blockchain.latest_block['transactions']]
            for vote in votes:
                label = tk.Label(self.master, text=vote)
                label.pack()

        # Print to terminal
        print("Blockchain Votes:")
        global block

        print(self.blockchain.current_transactions)
        for trns in (self.blockchain.current_transactions):
            print(f"Voter ID: {trns['voter_id']}, Voted for: {trns['candidate']}")

def main():
    blockchain = Blockchain()
    root = tk.Tk()
    app = VotingApp(root, blockchain)
    root.mainloop()

if __name__ == "__main__":
    main()
