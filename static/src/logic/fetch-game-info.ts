import axios, { AxiosResponse } from 'axios';
import { ProtectedError, GameInfoResponse } from '../types';
import protectedCall from './protected-call';

type ApiResponse = AxiosResponse<GameInfoResponse>;

interface ProtectedGameInfoResponse extends ProtectedError {
    data: GameInfoResponse | null;
}

interface ProtectedAxiosResponse extends ProtectedError {
    response: ApiResponse | null;
}

const baseURL = '/api/v1';
const api = axios.create({ baseURL });

const fetchGameInfo = async (): Promise<ProtectedGameInfoResponse> => {
    const { error, response }: ProtectedAxiosResponse = await protectedCall<ApiResponse>(api.get('/game_info'));
    const data = response ? response.data : null;
    return { error, data };
};

export default fetchGameInfo;
