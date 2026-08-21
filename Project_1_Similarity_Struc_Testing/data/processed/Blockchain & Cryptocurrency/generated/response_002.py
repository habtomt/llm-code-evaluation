from web3 import Web3
import json

class DecentralizedFinancePlatform :
    def __init__ (self ,contract_address ,contract_abi ,w3 ):

        self .contract_address =contract_address
        self .contract_abi =contract_abi
        self .w3 =w3
        self .contract =self .w3 .eth .contract (address =self .contract_address ,abi =self .contract_abi )

    def give_loan (self ,borrower ,amount ,interest ):

        try :

            account =self .w3 .eth .accounts [0 ]

            gas_estimate =self .contract .functions .giveLoan (borrower ,amount ,interest ).estimateGas ()

            tx =self .contract .functions .giveLoan (borrower ,amount ,interest ).buildTransaction ({
            'gas':gas_estimate ,
            'from':account ,
            'nonce':self .w3 .eth .getTransactionCount (account )
            })

            signed_tx =self .w3 .eth .account .sign_transaction (tx )

            tx_hash =self .w3 .eth .send_raw_transaction (signed_tx .rawTransaction )

            return tx_hash .hex ()
        except Exception as e :
            print (f"Error giving loan: {e}")
            return None

    def repay_loan (self ,amount ):

        try :

            account =self .w3 .eth .accounts [0 ]

            gas_estimate =self .contract .functions .repayLoan ().estimateGas ()

            tx =self .contract .functions .repayLoan ().buildTransaction ({
            'gas':gas_estimate ,
            'from':account ,
            'nonce':self .w3 .eth .getTransactionCount (account ),
            'value':amount
            })

            signed_tx =self .w3 .eth .account .sign_transaction (tx )

            tx_hash =self .w3 .eth .send_raw_transaction (signed_tx .rawTransaction )

            return tx_hash .hex ()
        except Exception as e :
            print (f"Error repaying loan: {e}")
            return None

with open ('contract_abi.json')as f :
    contract_abi =json .load (f )

w3 =Web3 (Web3 .HTTPProvider ('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))

contract_address ='0x...'

platform =DecentralizedFinancePlatform (contract_address ,contract_abi ,w3 )

borrower ='0x...'
amount =100
interest =10
tx_hash =platform .give_loan (borrower ,amount ,interest )
print (f"Loan given: {tx_hash}")

amount =110
tx_hash =platform .repay_loan (amount )
print (f"Loan repaid: {tx_hash}")