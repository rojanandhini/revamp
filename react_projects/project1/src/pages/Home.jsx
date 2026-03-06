import { Categories } from "../components/categoriesCard";
import { Hero } from "../components/hero";
import { ProductSection } from "../components/productCard";

export const Home=()=>{
  return(
    <div>
      <Hero/>
      <Categories/>
      <ProductSection/>
    </div>
  )
};