import React, { useEffect, useState } from 'react';
import { App as AntApp, Button, Badge } from 'antd';
import { SaveFilled } from '@ant-design/icons';
import TasksService from "../API/TasksService";
import { useFetching } from "../hooks/useFetching";


function SaverSelectedItems({ seletedItems, taskId, onSaved }) {
    const { message } = AntApp.useApp();
    const [isLoading, setIsLoading] = useState(false);
    const [fetchError, setError] = useState('');

    const saveSelectedItems = useFetching(async () => {
        console.log("saveSelectedItems", seletedItems)
        const response = await TasksService.saveAnnotatedTask(taskId, seletedItems)

        onSaved()
        message.success('Success!');
    }, setIsLoading, setError)

    return (
        <>
            <Button loading={isLoading} disabled={seletedItems.length == 0} onClick={saveSelectedItems} type="primary" icon={<SaveFilled />} >Save</Button>
        </>
    )
}

export default SaverSelectedItems