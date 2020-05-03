import fetchPaymentCode from '../logic/fetch-payment-code';
import confirmPaymentAndFetchGame from '../logic/fetch-payment-confirmation';
import { PaymentCodeData } from '../../../types';
import { protectedPayContract as payContract } from '../logic/pay-contract';
import * as constants from '../../../constants';

const processPaymentForUser = async (user: string): Promise<string> => {
    const { error: paymentCodeError, data: paymentCodeData } = await fetchPaymentCode();
    if (paymentCodeError) {
        return constants.FETCH_PAYMENT_CODE_ERROR;
    }
    const paymentCode = (paymentCodeData as PaymentCodeData).payment_code;
    const sessionId = (paymentCodeData as PaymentCodeData).session_id;

    const { error: transactionError } = await payContract(paymentCode);
    if (transactionError) {
        return constants.PAYMENT_CONFIRMATION_ERROR;
    }

    const { error: confirmationError } = await confirmPaymentAndFetchGame(user, sessionId);
    if (confirmationError) {
        return constants.PAYMENT_CONFIRMATION_ERROR;
    }
    return constants.PAYMENT_SUCCESS;
};

export default processPaymentForUser;
