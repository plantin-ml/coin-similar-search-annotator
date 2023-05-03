import { Table } from 'antd';
import { zonedTimeToUtc } from 'date-fns-tz';
import React, { useEffect, useState } from 'react';
import JobsService from '../../API/JobsService';
import { useFetching } from "../../hooks/useFetching";
import { Link } from "react-router-dom";


const columns = [
    {
        title: 'Alias',
        dataIndex: 'alias',
        key: 'alias'
    },
    {
        title: 'Total tasks',
        dataIndex: 'total_tasks',
        key: 'total_tasks',
        render: (text, record) => <Link to={`/tasks/job/${record.alias}`}>{text}</Link>,
    },
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: 'User assignee',
        dataIndex: 'user_assignee',
        key: 'user_assignee',
    },
    {
        title: 'Job type',
        dataIndex: 'job_type',
        key: 'job_type',
    },

    {
        title: 'Created at',
        dataIndex: 'created_at',
        key: 'created_at',
        render: (text, record) => zonedTimeToUtc(record.created_at, 'Europe/Moscow').toLocaleString(),
    },
]

const JobsTable = () => {
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
        const response = await JobsService.getAllJobs(
            tableParams.pagination.pageSize,
            (tableParams.pagination.current - 1) * tableParams.pagination.pageSize
        );
        setData(response.data.data.jobs);
        setTableParams({
            pagination: {
                ...tableParams.pagination,
                total: response.data.data.meta.total_jobs,
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

export default JobsTable;