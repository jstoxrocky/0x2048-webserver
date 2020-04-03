import axios, { AxiosResponse } from 'axios';
import { Protected, ChallengeData } from '../types';
import protectedCall from './protected-call';

const baseURL = '/';
const api = axios.create({ baseURL });

type ApiResponse = AxiosResponse<ChallengeData>;

interface ProtectedChallenge extends Protected {
    data: ChallengeData | null;
}

interface ProtectedAxiosResponse extends Protected {
    response: ApiResponse | null;
}

const fetchChallenge = async (): Promise<ProtectedChallenge> => {
    const errorMessage = 'There was an error retrieving the challenge';
    const { error, response }: ProtectedAxiosResponse = await protectedCall<ApiResponse>(
        api.get('/new_session'),
        errorMessage,
    );
    const data = response ? response.data : null;
    return { error, data };
};

export default fetchChallenge;
