import hashlib
import json
import time
import random


class BlockChain:
    def __init__(self):
        """
        owner_directory: A database of owners: properties stored in a dictionary
        transaction_lst: A list of transactions that have not been added to the chain yet.
        A transaction is of the form {'Seller': seller_name, 'Property': property_name, 'Buyer': buyer_name}
        chain: A list of blocks in the chain. Each block is a dictionary with the header keys and
        the list of transactions.
        nodes: The set of names of the users registered in the system.
        """
        self.owner_directory = {"zia": ["usa", "uk", "uae"], "gia": ["delhi", "bombay", "hyd"],
                                "tia": ["dc", "ny", "la"]}
        self.transaction_lst = []
        self.chain = []
        self.nodes = set(["zia", "gia", "tia"])
        self.initialize_genesis('1')

    def initialize_genesis(self, prevhash):
        """
        Initializes the Genisis Block and adds it to the chain.
        :param prevhash:
        :return: None
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': "No Transactions",
            'previous_hash': prevhash,
            'merkle root': hashlib.sha256(json.dumps(self.owner_directory, sort_keys=True).encode()).hexdigest(), # Hash of the initial owner_directory, in order to preserve it.
            'directory': self.owner_directory,
            'miner node': "Genesis Block",
        }
        self.chain.append(block)        # Adding block to the chain

    def register_node(self, name):
        """
        Adds the name of the new User to the set of nodes.
        :param name:
        :return: None
        """
        self.nodes.add(name)

    def assignTime(self):
        """
        Assigns random time to the miners and returns a list of miners in order of increasing time.
        :return: list
        """
        miner_lst = self.nodes
        time_lst = list()
        for i in miner_lst:
            rt = random.randint(1, len(miner_lst) ** 2)     # The upper limit could be anything greater than equal to the number of miners in order to avoid clashes.
            time_lst.append(rt)

        ziped = zip(time_lst, miner_lst)
        sort = sorted(ziped, reverse=False)         # Sorting the miners according to the time allotted.
        tuple_lst = zip(*sort)
        time_lst, miner_lst = [list(t) for t in tuple_lst]
        print("Miner order by time assigned: ", miner_lst)
        return miner_lst

    def verify_transaction(self, Seller, Property, Buyer):
        """
        Checks whether the transaction going to be added to block is valid or not.
        :param Seller: String
        :param Property: String
        :param Buyer: String
        :return: Boolean
        """
        if (Seller not in self.nodes or Buyer not in self.nodes):
            return False
        if (Property not in self.owner_directory[Seller]):
            return False
        return True

    @staticmethod
    def hash(block):
        """
        Given a dictionary the function returns its hash value.
        :param block:
        :return: hash value
        """
        block_str = json.dumps(block, sort_keys=True).encode()      # Converting the json/dictionary to a string before using sha256
        return hashlib.sha256(block_str).hexdigest()                # The SHA256 is one of the most efficient hashing functions out there.

    def get_merkle_root(self, transactions):
        """
        Function returns the collective hash value of the transactions using the merkle tree.
        NEW FEATURE:
        Passed in the owner_directory along with the transactions into the merkle tree to ensure immutability
        of the owner_directory in order to avoid malicious or faulty transactions to be added to the next block.
        :param transactions:
        :return: merkle root.
        """
        branches = [hashlib.sha256(json.dumps(t, sort_keys=True).encode()).hexdigest() for t in transactions]
        branches.append(hashlib.sha256(json.dumps(self.owner_directory, sort_keys=True).encode()).hexdigest())
        while len(branches) > 1:
            if (len(branches) % 2) == 1:        # Duplicating the last element in case of odd number of elements.
                branches.append(branches[-1])

            branches = [hashlib.sha256(a.encode() + b.encode()).hexdigest() for (a, b) in
                        zip(branches[0::2], branches[1::2])]    # Hashing two elements at a time in a bottom-up fashion.

        return branches[0]      # Returning the merkle root.

    def mineUsingPoET(self):
        """
        Transactions are verified and added into a block. The block in turn is added to the chain
        by the miner assigned via PoET (assign_Time).
        """
        curr_trans = self.transaction_lst   # curr_trans is a copy of all the transactions that have not been added to the chain.
        miner_lst = self.assignTime()   # miner_lst contains the miner names in order of assigned waiting time.
        count = 0
        max_trans = 3           # Setting an upper limit on the number of transactions in a block
        while len(curr_trans) != 0:
            if len(curr_trans) <= max_trans:
                lst = curr_trans        # In case the transactions are less than the upper limit
            else:
                lst = curr_trans[:max_trans]    # In case the transactions exceed the upper limit, a new lst of max_trans length is taken.
            for d in lst:
                if not self.verify_transaction(d['Seller'], d['Property'], d['Buyer']):     # In case the transaction is not valid, it is skipped and erased altogether.
                    print("Invalid Transaction: ", "")
                    print(d, "")
                    print("Transaction Aborted")
                    lst.remove(d)
                    continue
                self.owner_directory[d['Seller']].remove(d['Property'])     # In case of valid transactions, the owner_directory is updated as soon as the transaction is verified.
                self.owner_directory[d['Buyer']].append(d['Property'])
            if len(lst) != 0:
                temp_block = {
                    'index': len(self.chain) + 1,
                    'timestamp': time.time(),
                    'transactions': lst,
                    'previous_hash': self.hash(self.chain[-1]),
                    'merkle root': self.get_merkle_root(lst),
                    'directory': self.owner_directory,
                    'miner node': miner_lst[count % len(miner_lst)],    # The miners are given access on a rotational
                    # basis after the time assigned. This might occur in rare cases where the max_trans*no_of_miners
                    # is less than no_of_transactions
                }
                self.chain.append(temp_block)
                count += 1
            if len(curr_trans) <= max_trans:
                break
            curr_trans = curr_trans[max_trans:]
        self.transaction_lst = []       # transaction_lst is cleared

    def new_transaction(self, Seller, Property, Buyer):
        """
        Makes a transaction dictionary and append it to the transaction_lst.
        :param Seller: string
        :param Property: string
        :param Buyer: string
        :return: None
        """
        temp_transaction_block = {
            'Seller': Seller,
            'Property': Property,
            'Buyer': Buyer,
        }
        self.transaction_lst.append(temp_transaction_block)


if __name__ == '__main__':

    def register_node():
        """
        Takes a line with the first word as the user name and the rest of the words as
        names of the properties owned by the user.
        :return: response : dictionary giving information on the new user.
        """
        lst = input().split(" ")
        if "" in lst:
            print("Invalid Input, registration aborted.")
            return
        blockchain.register_node(lst[0])        # Updating the self.nodes
        blockchain.owner_directory[lst[0]] = lst[1:]    # Updating the self.owner_directory
        response = {
            'Message': 'New user has been added',
            'User_Name': lst[0],
            'User_Property': lst[1:]
        }
        print(response)
        return response

    def chainTranslation():
        """
        Returns the blockchain and its length
        """
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return response


    def new_transaction():
        """
        Takes input from the user regarding the new transaction.
        """
        print("Enter Seller ")
        s = input()
        print("Enter Property Name/ID ")
        p = input()
        print("Enter Buyer ")
        b = input()
        blockchain.new_transaction(s, p, b)     # Sends the inputs as parameters to the class method.


    def mine():
        """Calls the class method to start mining"""
        blockchain.mineUsingPoET()


    blockchain = BlockChain()
    while (True):
        print("<!==================================================================!>")
        print("1 Register New User")
        print("2 Display Blockchain")
        print("3 New Transaction")
        print("4 Mine")
        print("5 List The Current Transactions")
        print("6 Display Directory")
        print("7 View Transaction History for a Property")
        print("<!==================================================================!>")
        try:
            i = int(input())
        except:
            print("Invalid Input. Please enter a number.")
            continue
        if i > 7 or i < 1:
            print("Invalid Option")
        if i == 1:
            print("Enter New User Name Followed By Property Owned (Use single whitespace character space as delimiter)")
            register_node()

        elif i == 2:
            temp = chainTranslation()
            for k in temp['chain']:
                for l in k:
                    print(l, k[l])
                print("<!--------------------------------------------!>")
            print("Length of Blockchain = " + str(temp['length']))

        elif i == 3:
            new_transaction()

        elif i == 4:
            mine()
        elif i == 5:
            temp = blockchain.transaction_lst
            for i in temp:
                print(i)
        elif i == 6:
            print(blockchain.owner_directory)
        elif i == 7:
            print("Enter property name:")
            s = input()
            temp = chainTranslation()
            for k in temp['chain']:
                for l in k:
                    if l == 'transactions':
                        if (type(k[l]) == type([])):
                            for p in k[l]:
                                if type(p) == type({1: 2}):
                                    if p['Property'] == s:
                                        print(p)
                        break                               # Only transactions were needed of each block
                                                            # therefore skip to the next block
