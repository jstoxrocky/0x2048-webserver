import { createContext } from 'react';
import { Session } from './types';

const id = null;
const gamestate = null;
const signedScore = null;
const session: Session = { id, gamestate, signedScore };
const setSession: React.Dispatch<React.SetStateAction<Session>> = (v) => v;
const initialSessionContext = { session, setSession };
const SessionContext = createContext(initialSessionContext);

export default SessionContext;
