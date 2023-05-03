import {
    CarryOutOutlined,
    BarsOutlined,
    AppstoreOutlined
} from '@ant-design/icons';
import { Layout, Menu } from 'antd';
import React, { useState } from 'react';
import JobsTable from '../components/Jobs/JobsTable';

const { Footer, Header, Sider, Content } = Layout;

const JobsPage = () => {
    return (
        <JobsTable />
    );
};

export default JobsPage;