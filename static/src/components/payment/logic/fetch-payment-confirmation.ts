import axios, { AxiosResponse } from 'axios';
import Web3 from 'web3';
import { ProtectedError, Gamestate } from '../../../types';
import protectedCall from './protected-call';

type ApiResponse = AxiosResponse<Gamestate>;

interface ProtectedGamestate extends ProtectedError {
    data: Gamestate | null;
}

interface ProtectedAxiosResponse extends ProtectedError {
    response: ApiResponse | null;
}

const baseURL = '/api/v1';
const api = axios.create({ baseURL });

const confirmPaymentAndFetchGame = async (user: string, sessionId: string): Promise<ProtectedGamestate> => {
    const checksumAddress = Web3.utils.toChecksumAddress(user);
    const params = { user: checksumAddress, session_id: sessionId }; // eslint-disable-line @typescript-eslint/camelcase
    const { error, response }: ProtectedAxiosResponse = await protectedCall<ApiResponse>(
        api.get('/payment_confirmation', { params }),
    );
    const data = response ? response.data : null;
    return { error, data };
};

export default confirmPaymentAndFetchGame;
