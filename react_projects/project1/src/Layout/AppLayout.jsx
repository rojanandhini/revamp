import React from 'react'
import Header from '../components/header'
import { SearchBar } from '../components/searchBar'
import { Outlet } from 'react-router-dom'
import { Footer } from '../components/footer'

export const AppLayout = () => {
  return (
    <div>
          <Header/>
           <SearchBar/> 
          {/*<Hero/>
          <Categories/>
          <ProductSection/>*/}
          <div className="mt-40">
            <Outlet/>
          </div>
          <Footer/>
        </div>
  )
}
