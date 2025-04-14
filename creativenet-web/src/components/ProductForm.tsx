
export function ProductForm({ products, setProducts }) {
  const handleAdd = () => {
    setProducts([...products, {
      계약여부: "Y", 식별번호: "", 계약금액: "", 제품모델명: "", 품명: "",
      모델명: "", 규격: "", 수량: "", 원산지: "", 비고: ""
    }]);
  };

  return (
    <div>
      <button onClick={handleAdd} className="mb-2 px-4 py-2 bg-green-500 text-white rounded">
        제품 추가
      </button>
      {products.map((p, idx) => (
        <div key={idx} className="mb-2 border p-2 rounded bg-gray-100">
          <input placeholder="제품모델명" value={p.제품모델명} onChange={e => {
            const newP = [...products];
            newP[idx].제품모델명 = e.target.value;
            setProducts(newP);
          }} className="p-1 border w-full" />
        </div>
      ))}
    </div>
  );
}
