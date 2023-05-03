import { Badge, Button, Col, Image, Layout, Row, Select, Space, Spin, Tabs, Empty, Tag } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import TasksService from "../../API/TasksService";
import { useFetching } from "../../hooks/useFetching";
import GalleryCoins from '../GalleryCoins/GalleryCoins';
import SaverSelectedItems from "../SaverSelectedItems.jsx";
import NavigationToolBar from './NavigationToolBar';
import CoinCategory from '../CoinCategory.jsx';
import cl from "./Task.module.css";

const { Header, Content, Sider } = Layout;
const { Option } = Select;

const availableTags = [
  'investigation',
  'to_remove'
]

function TaskControll() {
  const { taskId } = useParams()
  const [limit, setLimit] = useState(5);
  const [task, setTask] = useState()
  const [galleryCoins, setGalleryCoins] = useState([])
  const [queryImg, setQueryImg] = useState()
  const [selectedCategory, setSelectedCategory] = useState()
  const [isLoading, setIsLoading] = useState(false);
  const [fetchError, setError] = useState('');
  let [selecteds, setSelecteds] = useState([]);
  const [tag, setTag] = useState();
  const [activeTabKey, setActiveTabKey] = useState('gallery')

  const fetchGalleryCoins = useFetching(async () => {

    if (taskId) {
      const response = await TasksService.getGalleryCoinsByTaskId(taskId, limit);

      setQueryImg(response.data.data.query_img)
      setGalleryCoins(response.data.data.gallery_coins)
    }
  }, setIsLoading, setError)


  const fetchTask = useFetching(async () => {
    const response = await TasksService.getTaskById(taskId);

    setTask(response.data.data)
    if (response.data.data.manual_annotation) {
      setSelecteds([...response.data.data.manual_annotation.image_ids.map(x => x)])
    }

  }, setIsLoading, setError)

  useEffect(() => {
    setActiveTabKey('gallery')
    setSelectedCategory(null)
    fetchTask()
  }, [taskId]);

  useEffect(() => {
    fetchGalleryCoins()
  }, [taskId, limit]);


  const onSelectItem = (coin) => {
    console.log('onSelectItem', coin)

    if (selecteds.includes(coin.id)) {
      setSelecteds([...selecteds.filter(item => item !== coin.id)])
    } else {
      setSelecteds([...selecteds, coin.id])
    }
  }

  const onSelectAllItems = (coins) => {
    selecteds = new Set([...selecteds, ...coins.map(coin => coin.id)])
    setSelecteds(Array.from(selecteds))
  }

  const handleSaveTag = async () => {
    if (!tag) {
      return;
    }

    const response = await TasksService.saveTag(taskId, tag);
    setTag(null);
    fetchTask()
  }

  const onSelectCategory = (categoryId) => {
    setActiveTabKey('by_category')
    setSelectedCategory(categoryId)
    console.log('onSelectCategory', categoryId)
  }

  const siderStyle = {
    lineHeight: '120px',
    color: '#fff',
    background: 'rgba(255, 255, 255, 0.2)',
    textAlign: 'center',
  };

  const contentStyle = {
    padding: '10px',
    color: '#fff',
  };
  const toolsBarStyle = {
    padding: '10px',
  };

  if (!task) {
    return <Empty/>;
  }

  const getTaskMetaInfo = (meta) => {
    return (
        <table className={ cl.tableMetaInformation } >
          <tbody>
            <tr>
              <td>ID</td>
              <td>{meta.coin_id}</td>
            </tr>
            <tr>
              <td>Country</td>
              <td>{meta.country}</td>
            </tr>
            <tr>
              <td>Side</td>
              <td>{meta.coin_side}</td>
            </tr>
            <tr>
              <td>Name</td>
              <td>{meta.name}</td>
            </tr>
            <tr>
              <td>Year</td>
              <td>{meta.year}</td>
            </tr>
            <tr>
              <td>Denomination</td>
              <td>{meta.denomination}</td>
            </tr>
            </tbody>
        </table>
    )
  }

  const getTabItems = () => {
    return [
      {
        key: 'gallery',
        label: `Gallery`,
        children: (
          <GalleryCoins
            onSelectCategory={onSelectCategory}
            coins={galleryCoins}
            onSelectAll={onSelectAllItems}
            onSelectItem={onSelectItem}
            selecteds={selecteds}
          />
        )
      },
      {
        key: 'by_category',
        label: `By category`,
        children: (
          <CoinCategory
            catId={selectedCategory}
            selecteds={selecteds}
            onSelectItem={onSelectItem}
          />
        )
      }
    ]
  }
  return (
    <>
      <Layout>
        {task && task.state == 'merged' && (
          <div style={{'backgroundColor': 'red', 'color': 'yellow', 'fontWeight': 'bold'}}>
              Already Merged!
          </div>
        )}

        <NavigationToolBar
          task={task}
          limit={limit}
          onChangeLimit={setLimit}
          isLoading={isLoading}
        />
        <Layout>
          <Sider style={siderStyle} width="224">
            {queryImg && (
              <>
                <Image src={`data:image/jpeg;base64,${queryImg}`} width={224} height={224} />
                {task && task.meta && getTaskMetaInfo(task.meta) }
                <Image src={task.url} width={224} height={224} />
              </>
            )}
          </Sider>
          <Content>
            <Row justify="left" style={toolsBarStyle}>
              <Col span={6}>
                <Space wrap>
                  Annotations: <Badge count={selecteds.length > 0 ? selecteds.length : 0} showZero color='#faad14' />
                  <SaverSelectedItems
                    seletedItems={[...selecteds]}
                    taskId={taskId}
                    onSaved={() => fetchTask()}
                  />
                </Space>
              </Col>
              <Col span={18}>
                <Space wrap>
                    {task.tags && task.tags.map(t => <Tag color="blue">{t}</Tag>)}
                    Tag:
                    <Select value={ tag } defaultValue="" style={{ width: 160 }} onChange={ setTag }>
                        { availableTags.map(k => <Option key={k} value={k}>{k}</Option> ) }
                    </Select>
                    <Button onClick={ handleSaveTag }>Save tag</Button>
                </Space>
              </Col>
            </Row>
            <Spin tip="Loading..." spinning={isLoading} size="large">
              <Content style={contentStyle}>
                <Tabs items={getTabItems()} defaultActiveKey="gallery" activeKey={ activeTabKey } onChange={ setActiveTabKey } />
              </Content>
            </Spin>
          </Content>
        </Layout>
      </Layout>
    </>
  )
}

export default TaskControll