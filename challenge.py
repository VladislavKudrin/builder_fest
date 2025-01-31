import os

from blockfrost import ApiUrls
from dotenv import load_dotenv
from pycardano import (
    Address,
    BlockFrostChainContext,
    DRep,
    DRepKind,
    Network,
    StakeCredential,
    TransactionBuilder,
    TransactionOutput,
    VerificationKeyHash,
    VoteDelegation,
)

load_dotenv(override=True)

BLOCKFROST_PROJECT_ID = os.getenv("BLOCKFROST_PROJECT_ID")
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
TO_ADDRESS = "addr1zyzpenlg0vywj7zdh9dzdeggaer94zvckfncv9c3886c36yafhxhu32dys6pvn6wlw8dav6cmp4pmtv7cc3yel9uu0nqhcjd29"
SEND_AMOUNT = "150000000"
DREP_VHASH = os.getenv("DREP_VHASH")

network = Network.MAINNET
context = BlockFrostChainContext(BLOCKFROST_PROJECT_ID, base_url=ApiUrls.mainnet.value)
full_address = Address.from_primitive(FROM_ADDRESS)
stake_address = Address(staking_part=full_address.staking_part, network=Network.MAINNET)

stake_creds = StakeCredential(stake_address.staking_part)
drep = DRep(
    DRepKind(0),
    VerificationKeyHash(bytes.fromhex(DREP_VHASH)),
)

vote_delegation_certificate = VoteDelegation(stake_creds, drep)

builder = TransactionBuilder(context, certificates=[vote_delegation_certificate])
builder.add_input_address(FROM_ADDRESS)

builder.add_output(
    TransactionOutput.from_primitive(
        [
            TO_ADDRESS,
            int(SEND_AMOUNT),
        ]
    )
)

builder.fee_buffer = 150000
tx = builder.build_and_sign([], change_address=FROM_ADDRESS)

print(tx.to_cbor().hex())
