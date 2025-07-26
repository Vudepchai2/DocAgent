from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from decimal import Decimal

class TxStatus(Enum):
    """
    ```Represents the various statuses a transaction can have.

        This enumeration defines the possible states of a transaction within the
        system, providing a standardized way to track and manage transaction
        outcomes. It is used to indicate the current status of a transaction,
        whether it is pending, completed, failed, or refunded.

        Description:
            The TxStatus enum is essential for transaction management, allowing
            systems to handle different transaction states consistently. It is
            particularly useful in financial systems, order processing, or any
            application where transaction tracking is necessary.

            This enum fits into the larger system architecture by providing a
            clear and concise way to represent transaction states, facilitating
            error handling, status updates, and reporting.

        Attributes:
            WAIT (str): Indicates that the transaction is pending.
            DONE (str): Indicates that the transaction has been completed successfully.
            ERR (str): Indicates that the transaction has failed.
            RET (str): Indicates that the transaction has been refunded.

        Example:
            # Example usage of TxStatus
            transaction_status = TxStatus.DONE
            if transaction_status == TxStatus.DONE:
                print("Transaction completed successfully.")
        ```
    """
    WAIT = 'pending'
    DONE = 'completed'
    ERR = 'failed'
    RET = 'refunded'

@dataclass
class Tx:
    """
    ```Represents a financial transaction with its details and status.

        This class encapsulates the information related to a transaction, including
        its unique identifier, amount, status, method of transaction, and an optional
        message. It is used to track and manage transactions within the system,
        providing a structured way to handle transaction data.

        Description:
            The Tx class is designed to facilitate the management of transactions
            by storing all relevant details in a single object. It is particularly
            useful in financial systems, e-commerce platforms, or any application
            where transaction tracking is essential.

            This class fits into the larger system architecture by serving as a
            data container for transaction operations, enabling easy access and
            manipulation of transaction details.

        Attributes:
            id (str): A unique identifier for the transaction.
            amt (Decimal): The amount involved in the transaction.
            st (TxStatus): The current status of the transaction, represented by
            the TxStatus enum.
            mth (str): The method used for the transaction (e.g., 'cash').
            msg (Optional[str]): An optional message providing additional information
            about the transaction, such as error details.

        Example:
            # Example usage of Tx
            transaction = Tx(id='T123', amt=Decimal('50.00'), st=TxStatus.DONE, mth='cash')
            print(f"Transaction {transaction.id} is {transaction.st.value}.")
        ```
    """
    id: str
    amt: Decimal
    st: TxStatus
    mth: str
    msg: Optional[str] = None

class Handler(ABC):
    """
    No docstring provided.
    """

    @abstractmethod
    def proc(self, amt: Decimal) -> Tx:
        """
        No docstring provided.
        """
        pass

    @abstractmethod
    def rev(self, tx: Tx) -> bool:
        """
        No docstring provided.
        """
        pass

class Cash(Handler):
    """
    No docstring provided.
    """

    def __init__(self):
        self.bal: Decimal = Decimal('0.00')

    def add(self, amt: Decimal) -> None:
        """
        ```Increase the cash balance by a specified amount.

            This method adds a given amount to the current cash balance. It is used
            to update the balance when additional funds are received or deposited.

            Args:
                amt (Decimal): The amount to be added to the balance. Must be a
                non-negative Decimal value.

            Usage:
                Use this method whenever you need to increase the cash balance,
                such as when processing deposits or receiving payments.

            Example:
                cash_handler = Cash()
                cash_handler.add(Decimal('100.00'))
                print(cash_handler.bal)  # Outputs: 100.00
            ```
        """
        self.bal += amt

    def proc(self, amt: Decimal) -> Tx:
        """
        ```Process a transaction by deducting the specified amount from the balance.

            This method attempts to deduct a given amount from the current cash balance
            and returns a transaction object indicating the result. If the balance is
            sufficient, the transaction is marked as completed; otherwise, it is marked
            as failed due to insufficient funds.

            Args:
                amt (Decimal): The amount to be deducted from the balance. Must be a
                non-negative Decimal value.

            Returns:
                Tx: A transaction object containing the transaction ID, amount, status,
                method, and an optional message. The status will be `TxStatus.DONE` if
                the transaction is successful, or `TxStatus.ERR` with a message if it fails.

            Usage:
                Use this method to process payments or withdrawals, ensuring that the
                balance is sufficient before completing the transaction.

            Example:
                cash_handler = Cash()
                transaction = cash_handler.proc(Decimal('50.00'))
                if transaction.st == TxStatus.DONE:
                    print("Transaction successful.")
                else:
                    print("Transaction failed:", transaction.msg)
            ```
        """
        if self.bal >= amt:
            self.bal -= amt
            return Tx(id=f'C_{id(self)}', amt=amt, st=TxStatus.DONE, mth='cash')
        return Tx(id=f'C_{id(self)}', amt=amt, st=TxStatus.ERR, mth='cash', msg='insufficient')

    def rev(self, tx: Tx) -> bool:
        """
        ```Reverse a completed transaction and update the balance accordingly.

            This method attempts to reverse a transaction that has been marked as completed.
            If successful, it restores the transaction amount to the balance and updates
            the transaction status to refunded.

            Args:
                tx (Tx): The transaction object to be reversed. The transaction must have
                a status of `TxStatus.DONE` to be eligible for reversal.

            Returns:
                bool: Returns `True` if the transaction was successfully reversed and the
                balance updated. Returns `False` if the transaction was not eligible for
                reversal (i.e., not completed).

            Usage:
                Use this method to handle transaction reversals, such as refunds or
                cancellations, ensuring that only completed transactions are reversed.

            Example:
                cash_handler = Cash()
                transaction = cash_handler.proc(Decimal('50.00'))
                if transaction.st == TxStatus.DONE:
                    success = cash_handler.rev(transaction)
                    if success:
                        print("Transaction reversed successfully.")
                    else:
                        print("Transaction reversal failed.")
            ```
        """
        if tx.st == TxStatus.DONE:
            self.bal += tx.amt
            tx.st = TxStatus.RET
            return True
        return False

    def ret(self) -> Decimal:
        """
        ```Return the current cash balance and reset it to zero.

            This method retrieves the current balance of cash and then resets the balance
            to zero. It is typically used to settle accounts or clear the balance at the
            end of a transaction cycle.

            Returns:
                Decimal: The cash balance before it was reset to zero.

            Usage:
                Use this method when you need to finalize transactions and clear the
                cash balance, such as during end-of-day processing or when closing
                a cash drawer.

            Example:
                cash_handler = Cash()
                cash_handler.add(Decimal('100.00'))
                balance = cash_handler.ret()
                print(balance)  # Outputs: 100.00
                print(cash_handler.bal)  # Outputs: 0.00
            ```
        """
        tmp = self.bal
        self.bal = Decimal('0.00')
        return tmp