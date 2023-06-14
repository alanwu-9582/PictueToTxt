# PNG2TEXTART 圖片轉文字圖

使用 Python 開發的圖像處理程式，可以將 PNG 圖像傳換為文字或是 ASCII 畫

## 使用說明
#### 載入圖片
點擊「剪貼簿」，可以從剪貼簿中載入圖片
#### 亮度值
可以調整兩個不同亮度的數值，程式會根據圖片像素深淺來條整輸出文字的深淺

點擊「調整數值」 程式將自動計算最適合的圖片亮度值

#### 壓縮量
調整「壓縮量」可以調整寬與高的比例

#### 縮放值
調整「縮放值」可以等比例縮放圖片

#### ASCII
如果勾選 ASCII 程式將不會根據顯示文字來輸出內容，而是使用多個不同密度的 ASCII 文字來輸出

#### 儲存
輸入儲存檔名後，按下「儲存輸出」按鈕，程式將轉換結果儲存為指定的檔案。

#### 重新載入圖片
如果從資料夾直接更換檔案，可以點擊「重載圖片」重新讀取一次資料夾中的照片

#### 設定
可以修改 `options.json` 中的資料，自訂義部份內容

## 注意事項
- 本程式僅支援 PNG 格式的圖片。
- 程式運行過程中請勿關閉主視窗。
