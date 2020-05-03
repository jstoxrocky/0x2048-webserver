import { ProtectedError } from '../../../types';

interface ProtectedCallResponse<T> extends ProtectedError {
    response: T | null;
}

const protectedCall = async <T>(promise: Promise<T>): Promise<ProtectedCallResponse<T>> => {
    return promise
        .then(
            (response: T): ProtectedCallResponse<T> => {
                return { error: false, response };
            },
        )
        .catch(
            (): Promise<ProtectedCallResponse<T>> => {
                return Promise.resolve({ error: true, response: null });
            },
        );
};

export default protectedCall;
