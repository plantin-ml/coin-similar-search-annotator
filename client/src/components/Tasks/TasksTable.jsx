import React, { useEffect, useState } from 'react';
import { Table, Image } from 'antd';
import TasksService from '../../API/TasksService';
import { Link } from "react-router-dom";
import { useFetching } from "../../hooks/useFetching";
import { zonedTimeToUtc } from 'date-fns-tz';
import { useParams } from "react-router-dom";


const columns = [
    {
        title: 'Alias',
        dataIndex: 'task_alias',
        key: 'task_alias',
        // sorter: (a, b) => a.task_alias.localeCompare(b.task_alias),

        render: (text, record) => <Link to={`/annotate/job/${record.job_alias}/task/${record.task_alias}`}>{text}</Link>,
        // width: '20%',
    },
    {
        title: 'Image',
        dataIndex: 'url',
        key: 'url',
        render: (text, record) => <Image src={record.url} width={32} height={32} />,
        // width: '20%',
    },
    {
        title: 'State',
        dataIndex: 'state',
        key: 'state',
    },
    {
        title: 'Coin side',
        dataIndex: 'coin_side',
        key: 'coin_side',
    },
    {
        title: 'Created at',
        dataIndex: 'created_at',
        key: 'created_at',
        render: (text, record) => zonedTimeToUtc(record.created_at, 'Europe/Moscow').toLocaleString(),
    },
]

const TasksTable = () => {
    const { jobAlias } = useParams()
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [tableParams, setTableParams] = useState({
        pagination: {
          current: 1,
          pageSize: 10,
        },
    });

    const fetchTasks = useFetching(async () => {
        const response = await TasksService.getAllTasks(
            jobAlias,
            tableParams.pagination.pageSize,
            (tableParams.pagination.current - 1) * tableParams.pagination.pageSize
        );
        setData(response.data.data.tasks);
        setTableParams({
            pagination: {
                ...tableParams.pagination,
                total: response.data.data.meta.total_tasks,
                pageSize: response.data.data.meta.limit,
                current: response.data.data.meta.offset / response.data.data.meta.limit + 1,
            }
        })
    }, setLoading, setError)

    useEffect(() => {
        fetchTasks()
    }, [JSON.stringify(tableParams)]);

    const handleTableChange = (pagination, filters, sorter) => {
        setTableParams({
          pagination,
          filters,
          ...sorter,
        });

        // `dataSource` is useless since `pageSize` changed
        if (pagination.pageSize !== tableParams.pagination?.pageSize) {
          setData([]);
        }
      };

    return (
        <Table
            rowKey={(record) => record.task_alias}
            dataSource={data}
            columns={columns}
            loading={loading}
            pagination={tableParams.pagination}
            onChange={handleTableChange}
        />
    );
};

export default TasksTable;