import React from 'react';
import { Text } from './styles/styles';
import * as copy from '../../../copy';

const PaymentSuccess = (): JSX.Element => {
    return <Text>{copy.PAYMENT_SUCCESS}</Text>;
};

export default PaymentSuccess;
