# PoET_Implementation
A python implementation of the Proof of Elapsed Time Consensus Algorithm for a Property Management System.
The System Uses Command-Line Interface. The options it provides are as follows:
1) Register New User
2) Display Blockchain
3) New Transaction
4) Mine
5) List the Current Transactions
6) Display Directory
7) View Transaction History for a Property

Documentation:
class BlockChain
   	 	Methods defined here:
__init__(self)
owner_directory: A database of owners: properties stored in a dictionary
transaction_lst: A list of transactions that have not been added to the chain
yet.
A transaction is of the form {'Seller': seller_name, 'Property': property_name, 'Buyer':
buyer_name}
chain: A list of blocks in the chain. Each block is a dictionary with the header keys and
the list of transactions.
nodes: The set of names of the users registered in the system.
assignTime(self)
Assigns random time to the miners and returns a list of miners in order of
increasing time.
:return: list
get_merkle_root(self, transactions)
Function returns the collective hash value of the transactions using the merkle tree.
NEW FEATURE:
Passed in the owner_directory along with the transactions into the merkle tree to ensure immutability
of the owner_directory in order to avoid malicious or faulty transactions to be added to the next block.
:param transactions:
:return: merkle root.
initialize_genesis(self, prevhash)
Initializes the Genisis Block and adds it to the chain.
:param prevhash:
:return: None
mineUsingPoET(self)
Transactions are verified and added into a block. The block in turn is added to the chain
by the miner assigned via PoET (assign_Time).
new_transaction(self, Seller, Property, Buyer)
Makes a transaction dictionary and append it to the transaction_lst.
:param Seller: string
:param Property: string
:param Buyer: string
:return: None
register_node(self, name)
Adds the name of the new User to the set of nodes.
:param name:
:return: None
verify_transaction(self, Seller, Property, Buyer)
Checks whether the transaction going to be added to block is valid or not.
:param Seller: String
:param Property: String
:param Buyer: String
:return: Boolean
________________________________________
Static methods defined here:
hash(block)
Given a dictionary the function returns its hash value.
:param block:
:return: hash value


