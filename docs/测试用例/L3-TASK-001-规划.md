# L3-TASK-001 Calculator-Tools MVP 站点测试规划

## 关联信息
- Issue: #1 验证 calculator-tools MVP 站点
- 站点地址: https://calculator-tools.todonot.com/
- Quality Hub project_id: 11949495-1428-4ae2-bbfd-0f10f4fc54a9
- Quality Hub run_id: 9e9d19c3-bff8-440c-a902-a4edc5622334

## 用例清单

### TC-001 [Type-A] [路由] 首页可访问（重定向到 /en/）
- 断言: `curl -sf https://calculator-tools.todonot.com/ | grep -q 'url=/en/'`
- 预期: HTTP 200，页面含 meta refresh 重定向到 /en/

### TC-002 [Type-A] [多语言] 英文首页含 CalcTools 标题和计算器列表
- 断言: `curl -sf https://calculator-tools.todonot.com/en/ | grep -q 'CalcTools' && curl -sf https://calculator-tools.todonot.com/en/ | grep -q 'calc-card'`
- 预期: HTTP 200，含 CalcTools 标题和多个计算器卡片链接

### TC-003 [Type-A] [多语言] 中文首页含中文内容
- 断言: `curl -sf https://calculator-tools.todonot.com/zh/ | grep -q '免费在线计算器'`
- 预期: HTTP 200，含中文标题和中文内容

### TC-004 [Type-A] [计算器] BMI 计算器页面可交互
- 断言: `curl -sf https://calculator-tools.todonot.com/en/bmi/ | grep -q 'calcBMI'`
- 预期: HTTP 200，含 height/weight 输入框、Calculate BMI 按钮和 calcBMI() 函数

### TC-005 [Type-A] [计算器] 贷款计算器页面可交互
- 断言: `curl -sf https://calculator-tools.todonot.com/zh/loan/ | grep -q 'calcLoan'`
- 预期: HTTP 200，含贷款金额/利率/期限输入框和 calcLoan() 函数

### TC-006 [Type-A] [静态资源] style.css 可访问
- 断言: `curl -sf https://calculator-tools.todonot.com/static/style.css | grep -q ':root'`
- 预期: HTTP 200，返回有效 CSS 内容

### TC-007 [Type-A] [SEO] sitemap.xml 可访问且为 XML 格式
- 断言: `curl -sf https://calculator-tools.todonot.com/sitemap.xml | grep -q '<urlset'`
- 预期: HTTP 200，返回有效 XML sitemap，含中英文 URL 条目

## 分组
- 全部为 Type-A（API/curl 验证），无依赖关系，可并行执行
- 执行时间预估: 每个用例 < 5 秒，总计 < 30 秒
