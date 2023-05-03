import { Input, Layout, Space, Spin } from 'antd';
import React, { useEffect, useState } from 'react';
import CoinDataService from "../API/CoinDataService";
import { useFetching } from "../hooks/useFetching";
import GalleryCoins from './GalleryCoins/GalleryCoins';

const { Header, Content, Sider } = Layout;
const { Search } = Input;

function CoinCategory({ catId, selecteds, onSelectItem }) {
  let [galleryCoins, setGalleryCoins] = useState([]);
  let [categoryId, setCategoryId] = useState();
  let [searchValue, setSearchValue] = useState();
  const [isLoading, setIsLoading] = useState(false);
  const [fetchError, setError] = useState('');

  const fetchCoins = useFetching(async () => {

    if (categoryId) {
      // setSelecteds([])
      const response = await CoinDataService.getAllByCoinId(categoryId);
      setGalleryCoins(response.data.data)
      // console.log(galleryCoins)
    }
  }, setIsLoading, setError)

  useEffect(() => {
    fetchCoins()
  }, [categoryId])

  useEffect(() => {
    setGalleryCoins([])
    setCategoryId(catId)
    setSearchValue(catId)
  }, [catId])

  const onSearch = (value) => {
    setCategoryId(parseInt(value))
  };
  return (
    <>
      <Space direction="vertical" style={{ width: '100%' }} size={[0, 48]}>
        <Layout>
          <Search value={searchValue} placeholder="category ID" onChange={(e) => { setSearchValue(e.target.value) }} onSearch={onSearch} style={{ 'width': '140px', 'marginBottom': '20px' }} />
          <Spin tip="Loading..." spinning={isLoading} size="large">
            <GalleryCoins coins={galleryCoins} onSelectItem={onSelectItem} selecteds={selecteds} />
          </Spin>
        </Layout>
      </Space>
    </>
  )
}

export default CoinCategory