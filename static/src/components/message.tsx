import React, { useContext } from 'react';
import sessionContext from '../session-context';

const Message = (): JSX.Element => {
    console.log('Message');
    const { session } = useContext(sessionContext);
    return <div>Message: {session.message}</div>;
};

export default Message;
