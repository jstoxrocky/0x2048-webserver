import { createContext } from 'react';
import { Session } from './types';
import { emptySession } from './empty-types';

const setSession: React.Dispatch<React.SetStateAction<Session>> = (v) => v;
const initialSessionContext = { session: emptySession, setSession };
export const SessionContext = createContext(initialSessionContext);

const setStage: React.Dispatch<React.SetStateAction<string>> = (v) => v;
const stage = '';
const initialStageContext = { stage, setStage };
export const StageContext = createContext(initialStageContext);

const setUser: React.Dispatch<React.SetStateAction<string>> = (v) => v;
const user = '';
const initialUserContext = { user, setUser };
export const UserContext = createContext(initialUserContext);
