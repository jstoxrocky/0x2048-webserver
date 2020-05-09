import fetchPaymentCode from './fetch-payment-code';
import confirmPaymentAndFetchGame from './fetch-payment-confirmation';
import { PaymentCodeData, Gamestate } from '../../../types';
import { protectedPayContract as payContract } from './pay-contract';
import * as constants from '../../../constants';

interface PaymentProcessingResponse {
    stage: string;
    gamestate: Gamestate | null;
}

const processPaymentForUser = async (user: string): Promise<PaymentProcessingResponse> => {
    const { error: paymentCodeError, data: paymentCodeData } = await fetchPaymentCode();
    if (paymentCodeError) {
        return { stage: constants.FETCH_PAYMENT_CODE_ERROR, gamestate: null };
    }
    const paymentCode = (paymentCodeData as PaymentCodeData).payment_code;
    const sessionId = (paymentCodeData as PaymentCodeData).session_id;

    const { error: transactionError } = await payContract(paymentCode);
    if (transactionError) {
        return { stage: constants.PAYMENT_CONFIRMATION_ERROR, gamestate: null };
    }

    const { error: confirmationError, data: gamestate } = await confirmPaymentAndFetchGame(user, sessionId);
    if (confirmationError) {
        return { stage: constants.PAYMENT_CONFIRMATION_ERROR, gamestate: null };
    }
    return { stage: constants.PAYMENT_SUCCESS, gamestate };
};

export default processPaymentForUser;
