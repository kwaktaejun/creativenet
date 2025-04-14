
export function MemoInput({ memo, setMemo }) {
  return (
    <div>
      <textarea
        value={memo}
        onChange={(e) => setMemo(e.target.value)}
        placeholder="이번 업로드에 대한 메모를 입력하세요"
        className="w-full p-2 border rounded"
      />
    </div>
  );
}
