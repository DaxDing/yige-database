-- ============================================================
-- 窗口函数对比演示
-- 用途: 验证原逻辑 vs 修复逻辑的差异
-- ============================================================

-- 创建测试数据：60 天，每天消费 100 元
WITH test_data AS (
    SELECT
        '123' AS creativity_id,
        TO_CHAR(DATEADD(TO_DATE('20260101', 'yyyymmdd'), day_offset, 'dd'), 'yyyymmdd') AS ds,
        100 AS fee
    FROM (
        SELECT ROW_NUMBER() OVER () - 1 AS day_offset
        FROM (
            SELECT * FROM VALUES (1),(1),(1),(1),(1),(1),(1),(1),(1),(1) -- 10行
        ) t1, (
            SELECT * FROM VALUES (1),(1),(1),(1),(1),(1) -- 6行
        ) t2
        LIMIT 60
    )
)

-- 对比两种窗口函数
SELECT
    ds,
    fee,

    -- 原逻辑：全量累计（无窗口边界）
    SUM(fee) OVER (
        PARTITION BY creativity_id
        ORDER BY ds
    ) AS original_累计值,

    -- 修复后：30天滚动窗口
    SUM(fee) OVER (
        PARTITION BY creativity_id
        ORDER BY ds
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS fixed_30天滚动值,

    -- 差异
    SUM(fee) OVER (PARTITION BY creativity_id ORDER BY ds)
    - SUM(fee) OVER (PARTITION BY creativity_id ORDER BY ds ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
    AS 差异

FROM test_data
WHERE ds IN ('20260101', '20260115', '20260130', '20260131', '20260201', '20260301')
ORDER BY ds;

-- ============================================================
-- 预期结果:
--
-- ds          fee  original  fixed  差异
-- ------------------------------------------------
-- 20260101    100    100      100     0
-- 20260115    100   1500     1500     0
-- 20260130    100   3000     3000     0
-- 20260131    100   3100     3000   100  ← 从这里开始有差异
-- 20260201    100   3200     3000   200  ← 差异继续扩大
-- 20260301    100   6000     3000  3000  ← 60天 vs 30天
-- ============================================================
