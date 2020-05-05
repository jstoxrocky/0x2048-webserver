import React, { useState } from 'react';
import { SessionContext } from '../contexts';
import { Session } from '../types';
import { emptySession } from '../empty-types';
import Header from './header';
// import Game from './game';
import Payment from './payment/payment';

const App = (): JSX.Element => {
    const [session, setSession] = useState<Session>(emptySession);
    const sessionValue = { session, setSession };
    return (
        <>
            <SessionContext.Provider value={sessionValue}>
                <Header />
                <Payment />
            </SessionContext.Provider>
        </>
    );
};

export default App;
