import React, { useState } from 'react';
import { ThemeProvider } from 'styled-components';
import sessionIdContext from '../session-context';
import Message from './message';
import NewGame from './new-game';

const theme = {
    backgroundColor: '#fff1e5',
    buttonBackgroundColor: '#f2dfce',
    buttonHoverBackgroundColor: '#66605c',
    fontFamily: 'sans-serif',
    fontSize: '1.3rem',
};

const App = (): JSX.Element => {
    console.log('App');
    const id = 'Loading...';
    const message = 'All good';
    const initialSession = { id, message };
    const [session, setSession] = useState(initialSession);
    const value = { session, setSession };
    return (
        <>
            <ThemeProvider theme={theme}>
                <sessionIdContext.Provider value={value}>
                    <Message />
                    <NewGame />
                </sessionIdContext.Provider>
            </ThemeProvider>
        </>
    );
};

export default App;
