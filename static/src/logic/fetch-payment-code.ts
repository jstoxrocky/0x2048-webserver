import axios, { AxiosResponse } from 'axios';
import { ProtectedError, PaymentCodeData } from '../types';
import protectedCall from './protected-call';

type ApiResponse = AxiosResponse<PaymentCodeData>;

interface ProtectedPaymentCode extends ProtectedError {
    data: PaymentCodeData | null;
}

interface ProtectedAxiosResponse extends ProtectedError {
    response: ApiResponse | null;
}

const baseURL = '/api/v1';
const api = axios.create({ baseURL });

const fetchPaymentCode = async (): Promise<ProtectedPaymentCode> => {
    const { error, response }: ProtectedAxiosResponse = await protectedCall<ApiResponse>(api.get('/payment_code'));
    const data = response ? response.data : null;
    return { error, data };
};

export default fetchPaymentCode;
