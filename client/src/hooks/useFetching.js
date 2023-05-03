import {useState} from "react";
import { App as AntApp} from 'antd';


export const useFetching = (callback, setIsLoading, setError) => {
    const { message } = AntApp.useApp();

    const fetching = async (...args) => {
        try {
            setIsLoading(true)
            setError('')
            await callback(...args)
        } catch (e) {
            setError(e.message);
            message.error(e.message);
        } finally {
            setIsLoading(false)
        }
    }

    return fetching
}
