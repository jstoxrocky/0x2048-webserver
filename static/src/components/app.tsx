import React, { useState } from 'react';
import SessionContext from '../session-context';
import PaymentProcessor from './payment-processor';
import { Session } from '../types';
import Header from './header';
import Game from './game';

const App = (): JSX.Element => {
    const [id, gamestate, signedScore] = [null, null, null];
    const initialSession: Session = { id, gamestate, signedScore };
    const [session, setSession] = useState<Session>(initialSession);
    const sessionValue = { session, setSession };
    return (
        <>
            <Header />
            <SessionContext.Provider value={sessionValue}>
                <PaymentProcessor />
            </SessionContext.Provider>
            <Game />
        </>
    );
};

export default App;
