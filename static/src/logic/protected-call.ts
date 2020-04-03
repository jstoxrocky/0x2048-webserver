import { Protected } from '../types';

interface ProtectedCallResponse<T> extends Protected {
    response: T | null;
}

const protectedCall = async <T>(promise: Promise<T>, message: string): Promise<ProtectedCallResponse<T>> => {
    return promise
        .then(
            (response: T): ProtectedCallResponse<T> => {
                return { error: null, response };
            },
        )
        .catch(
            (): Promise<ProtectedCallResponse<T>> => {
                return Promise.resolve({ error: message, response: null });
            },
        );
};

export default protectedCall;
