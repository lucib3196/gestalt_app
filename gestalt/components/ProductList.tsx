'use client';
// This is just a testing function



import { DataRenderer } from "./DataRenderer";


function ProductList(){
    const staticProducts = [
        { id: 1, name: 'Laptop', price: 999 },
        { id: 2, name: 'Phone', price: 699 }
    ];

    return (
        <div>
            <h2>Products</h2>
            <DataRenderer source = {staticProducts}>
                {(products)=>(
                    <div>
                        {products.map(product =>(
                            <>
                            <h3>{product.name}</h3>
                            <p>{product.price}</p>
                            </>
                        ))}
                    </div>
                )}
            </DataRenderer>
        </div>
    )
}

export default ProductList