import { test, expect } from '@playwright/test';

test.describe('首页', () => {
  test('中文首页加载并显示所有计算器卡片', async ({ page }) => {
    await page.goto('/zh/');
    await expect(page.locator('h1')).toHaveText('免费在线计算器');
    const cards = page.locator('.calc-card');
    await expect(cards).toHaveCount(9);
  });

  test('英文首页加载并显示所有计算器卡片', async ({ page }) => {
    await page.goto('/en/');
    await expect(page.locator('h1')).toHaveText('Free Online Calculators');
    const cards = page.locator('.calc-card');
    await expect(cards).toHaveCount(9);
  });

  test('导航栏 logo 存在', async ({ page }) => {
    await page.goto('/en/');
    await expect(page.locator('.logo')).toBeVisible();
    await expect(page.locator('.logo')).toContainText('CalcTools');
  });

  test('语言切换', async ({ page }) => {
    await page.goto('/en/');
    await page.click('a[href="/zh/"]');
    await expect(page).toHaveURL(/\/zh\//);
  });
});

test.describe('BMI 计算器', () => {
  test('计算 BMI 并显示结果', async ({ page }) => {
    await page.goto('/en/bmi/');
    await page.fill('#height', '170');
    await page.fill('#weight', '70');
    await page.click('button.btn');
    const result = page.locator('#result');
    await expect(result).toContainText('24.2');
    await expect(result).toContainText('Normal weight');
  });

  test('肥胖 BMI', async ({ page }) => {
    await page.goto('/en/bmi/');
    await page.fill('#height', '170');
    await page.fill('#weight', '90');
    await page.click('button.btn');
    await expect(page.locator('#result')).toContainText('Obese');
  });
});

test.describe('年龄计算器', () => {
  test('计算年龄并显示年月日', async ({ page }) => {
    await page.goto('/en/age/');
    await page.fill('#dob', '1990-01-15');
    await page.click('button.btn');
    const result = page.locator('#result');
    await expect(result).toContainText('years');
    await expect(result).toContainText('days');
  });
});

test.describe('折扣计算器', () => {
  test('计算折扣价格', async ({ page }) => {
    await page.goto('/en/discount/');
    await page.fill('#origPrice', '100');
    await page.fill('#discPct', '30');
    await page.click('button.btn');
    const result = page.locator('#result');
    await expect(result).toContainText('$30.00');
    await expect(result).toContainText('$70.00');
  });
});

test.describe('贷款计算器', () => {
  test('计算月供', async ({ page }) => {
    await page.goto('/en/loan/');
    await page.fill('#principal', '200000');
    await page.fill('#rate', '5.5');
    await page.fill('#years', '30');
    await page.click('button.btn');
    const result = page.locator('#result');
    await expect(result).toContainText('Monthly Payment');
    await expect(result).toContainText('$1135.58');
  });
});

test.describe('百分比计算器', () => {
  test('计算百分比', async ({ page }) => {
    await page.goto('/en/percentage/');
    await page.fill('#pct', '15');
    await page.fill('#num', '200');
    await page.click('button.btn:first-of-type');
    await expect(page.locator('#result1')).toContainText('30');
  });

  test('计算百分比变化', async ({ page }) => {
    await page.goto('/en/percentage/');
    await page.fill('#oldVal', '80');
    await page.fill('#newVal', '100');
    await page.locator('button.btn', { hasText: 'Calculate Change' }).click();
    await expect(page.locator('#result2')).toContainText('25.00%');
    await expect(page.locator('#result2')).toContainText('increase');
  });
});

test.describe('温度换算器', () => {
  test('摄氏度转换', async ({ page }) => {
    await page.goto('/en/temperature/');
    await page.fill('#tempVal', '100');
    await page.selectOption('#tempUnit', 'C');
    await page.click('button.btn');
    const result = page.locator('#result');
    await expect(result).toContainText('212.00 °F');
    await expect(result).toContainText('373.15 K');
  });

  test('华氏度转换', async ({ page }) => {
    await page.goto('/en/temperature/');
    await page.fill('#tempVal', '32');
    await page.selectOption('#tempUnit', 'F');
    await page.click('button.btn');
    await expect(page.locator('#result')).toContainText('0.00 °C');
  });
});

test.describe('小费计算器', () => {
  test('计算小费和分账', async ({ page }) => {
    await page.goto('/en/tip/');
    await page.fill('#billAmt', '100');
    await page.fill('#tipPct', '18');
    await page.fill('#people', '2');
    await page.click('button.btn');
    const result = page.locator('#result');
    await expect(result).toContainText('$18.00');
    await expect(result).toContainText('$59.00');
  });
});

test.describe('长度单位换算器', () => {
  test('米转英尺', async ({ page }) => {
    await page.goto('/en/unit-length/');
    await page.fill('#fromVal', '1');
    await page.selectOption('#fromUnit', 'm');
    await page.selectOption('#toUnit', 'ft');
    await page.click('button.btn');
    await expect(page.locator('#result')).toContainText('3.28084');
  });
});

test.describe('重量单位换算器', () => {
  test('千克转磅', async ({ page }) => {
    await page.goto('/en/unit-weight/');
    await page.fill('#wVal', '1');
    await page.selectOption('#wFrom', 'kg');
    await page.selectOption('#wTo', 'lb');
    await page.click('button.btn');
    await expect(page.locator('#result')).toContainText('2.20462');
  });
});
