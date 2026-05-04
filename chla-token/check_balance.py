import os
from web3 import Web3

# เชื่อมต่อกับ Anvil (Local Node)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# ข้อมูล CHELA Network
token_address = '0x7bA3EfA6ecd194bEeBcD5d91D62f0DF5C6ecB4a4'
treasury_wallet = '0x2Eeb0f207C8CF5Fe5F74F50D54572183FDF1087c'

# ERC20 BalanceOf ABI
abi = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

if w3.is_connected():
    contract = w3.eth.contract(address=token_address, abi=abi)
    balance = contract.functions.balanceOf(treasury_wallet).call()
    
    print(f"\n✅ Connected to CHELA Local Network")
    print(f"------------------------------------")
    print(f"CHELA Treasury Balance: {balance / 10**18:,.2f} CHLA")
    print(f"------------------------------------\n")
else:
    print("❌ Failed to connect to Anvil. Please make sure anvil is running.")
