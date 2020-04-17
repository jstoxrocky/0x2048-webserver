import axios, { AxiosResponse } from 'axios';
import Web3 from 'web3';
import { ProtectedError, GameResponse } from '../types';
import protectedCall from './protected-call';

type ApiResponse = AxiosResponse<GameResponse>;

interface ProtectedGameResponse extends ProtectedError {
    data: GameResponse | null;
}

interface ProtectedAxiosResponse extends ProtectedError {
    response: ApiResponse | null;
}

const baseURL = '/api/v1';
const api = axios.create({ baseURL });

const confirmPaymentAndFetchGame = async (address: string, sessionId: string): Promise<ProtectedGameResponse> => {
    const checksumAddress = Web3.utils.toChecksumAddress(address);
    const params = { address: checksumAddress, session_id: sessionId }; // eslint-disable-line @typescript-eslint/camelcase
    const { error, response }: ProtectedAxiosResponse = await protectedCall<ApiResponse>(api.get('/game', { params }));
    const data = response ? response.data : null;
    return { error, data };
};

export default confirmPaymentAndFetchGame;
