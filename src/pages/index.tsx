
import { useState } from "react";
import { UploadForm } from "../components/UploadForm";
import { ProductForm } from "../components/ProductForm";
import { MemoInput } from "../components/MemoInput";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [memo, setMemo] = useState("");

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-xl font-bold">크리에이티브넷 제품 등록</h1>
      <MemoInput memo={memo} setMemo={setMemo} />
      <ProductForm products={products} setProducts={setProducts} />
      <UploadForm products={products} memo={memo} />
    </div>
  );
}
