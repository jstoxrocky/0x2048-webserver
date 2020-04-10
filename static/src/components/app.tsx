import React, { useState } from 'react';
import { ThemeProvider } from 'styled-components';
import SessionContext from '../session-context';
import PaymentProcessor from './payment-processor';
import { Session } from '../types';
import Header from './header';
import Game from './game';

const theme = {
    backgroundColor: '#fff1e5',
    fontSize: '1.3rem',
    fontFamily: 'system-ui',
};

const App = (): JSX.Element => {
    const [id, gamestate, signedScore] = [null, null, null];
    const initialSession: Session = { id, gamestate, signedScore };
    const [session, setSession] = useState<Session>(initialSession);
    const sessionValue = { session, setSession };
    return (
        <>
            <ThemeProvider theme={theme}>
                <Header />
                <SessionContext.Provider value={sessionValue}>
                    <PaymentProcessor />
                </SessionContext.Provider>
                <Game gamestate={session.gamestate} />
            </ThemeProvider>
        </>
    );
};

export default App;
