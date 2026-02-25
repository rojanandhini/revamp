import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Header from './components/header'
import { Hero } from "./components/hero";
import { Categories, CategoryItems} from "./components/categoriesCard";
import { Footer } from "./components/footer";
import { SearchBar } from "./components/searchBar";
import { ProductCard, ProductSection } from "./components/productCard";

// eslint-disable-next-line react-refresh/only-export-components
const AppLayout=()=>{
  return(
    <div>
      <Header/>
      <SearchBar/>
      <Hero/>
      <Categories/>
      <ProductSection/>
      <Footer/>
    </div>
  );
};

const reactRoot= ReactDOM.createRoot(document.getElementById("root"));
reactRoot.render(<AppLayout/>);
 
