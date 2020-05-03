import axios, { AxiosResponse } from 'axios';
import { ProtectedError, Metadata } from '../../../types';
import protectedCall from './protected-call';

type ApiResponse = AxiosResponse<Metadata>;

interface ProtectedMetadata extends ProtectedError {
    data: Metadata | null;
}

interface ProtectedAxiosResponse extends ProtectedError {
    response: ApiResponse | null;
}

const baseURL = '/api/v1';
const api = axios.create({ baseURL });

const fetchMetadata = async (): Promise<ProtectedMetadata> => {
    const { error, response }: ProtectedAxiosResponse = await protectedCall<ApiResponse>(api.get('/metadata'));
    const data = response ? response.data : null;
    return { error, data };
};

export default fetchMetadata;
