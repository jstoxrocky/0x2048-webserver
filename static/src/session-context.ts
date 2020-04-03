import { createContext } from 'react';

interface Session {
    id: string;
    message: string;
}

const id = '';
const message = '';
const session = { id, message };
const setSession: React.Dispatch<React.SetStateAction<Session>> = (v) => v;
const initialSessionIdContext = { session, setSession };
const sessionContext = createContext(initialSessionIdContext);

export default sessionContext;
