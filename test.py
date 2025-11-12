"""
Stork Bot 测试脚本
用于测试核心功能的简单 demo
"""

import asyncio
from aiohttp import ClientSession, ClientTimeout
from colorama import Fore, Style
from datetime import datetime
import pytz

# 设置时区
wib = pytz.timezone('Asia/Jakarta')


class StorkTestDemo:
    """Stork Bot 测试类 - 用于演示核心功能"""

    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def log(self, message):
        """打印带时间戳的日志"""
        timestamp = datetime.now().astimezone(wib).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {timestamp} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        """显示欢迎信息"""
        print(f"""
{Fore.GREEN + Style.BRIGHT}╔═══════════════════════════════════════╗
║     Stork Bot 测试 Demo               ║
║     用于测试核心功能                   ║
╚═══════════════════════════════════════╝{Style.RESET_ALL}
        """)

    async def test_network_connection(self):
        """测试网络连接"""
        self.log(f"{Fore.YELLOW}测试网络连接...{Style.RESET_ALL}")

        try:
            async with ClientSession(timeout=ClientTimeout(total=10)) as session:
                async with session.get("https://httpbin.org/ip") as response:
                    if response.status == 200:
                        data = await response.json()
                        self.log(
                            f"{Fore.GREEN}✓ 网络连接正常{Style.RESET_ALL} "
                            f"- IP: {Fore.WHITE + Style.BRIGHT}{data.get('origin', 'N/A')}{Style.RESET_ALL}"
                        )
                        return True
                    else:
                        self.log(f"{Fore.RED}✗ 网络连接失败 - 状态码: {response.status}{Style.RESET_ALL}")
                        return False
        except Exception as e:
            self.log(f"{Fore.RED}✗ 网络连接异常: {str(e)}{Style.RESET_ALL}")
            return False

    async def test_proxy_format(self, proxy_string):
        """测试代理格式"""
        self.log(f"{Fore.YELLOW}测试代理格式: {proxy_string}{Style.RESET_ALL}")

        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxy_string.startswith(scheme) for scheme in schemes):
            self.log(f"{Fore.GREEN}✓ 代理格式正确{Style.RESET_ALL}")
            return proxy_string
        else:
            formatted = f"http://{proxy_string}"
            self.log(f"{Fore.YELLOW}⚠ 代理格式已自动修正为: {formatted}{Style.RESET_ALL}")
            return formatted

    async def test_token_masking(self, token):
        """测试 Token 掩码功能"""
        self.log(f"{Fore.YELLOW}测试 Token 掩码功能...{Style.RESET_ALL}")

        if len(token) > 6:
            masked = token[:3] + '*' * 6 + token[-3:]
            self.log(
                f"{Fore.GREEN}✓ 原始 Token: {Fore.WHITE}{token}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.GREEN}✓ 掩码后: {Fore.WHITE + Style.BRIGHT}{masked}{Style.RESET_ALL}"
            )
            return masked
        else:
            self.log(f"{Fore.RED}✗ Token 长度不足{Style.RESET_ALL}")
            return token

    async def test_concurrent_tasks(self):
        """测试并发任务"""
        self.log(f"{Fore.YELLOW}测试并发任务执行...{Style.RESET_ALL}")

        async def task(task_id, delay):
            await asyncio.sleep(delay)
            return f"任务 {task_id} 完成 (延迟 {delay}s)"

        tasks = [
            asyncio.create_task(task(1, 1)),
            asyncio.create_task(task(2, 2)),
            asyncio.create_task(task(3, 1.5))
        ]

        results = await asyncio.gather(*tasks)

        for result in results:
            self.log(f"{Fore.GREEN}✓ {result}{Style.RESET_ALL}")

    async def run_all_tests(self):
        """运行所有测试"""
        self.welcome()

        # 测试 1: 网络连接
        await self.test_network_connection()
        await asyncio.sleep(1)

        # 测试 2: 代理格式
        test_proxies = [
            "http://127.0.0.1:8080",
            "192.168.1.1:3128",
            "socks5://proxy.example.com:1080"
        ]
        for proxy in test_proxies:
            await self.test_proxy_format(proxy)
        await asyncio.sleep(1)

        # 测试 3: Token 掩码
        test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        await self.test_token_masking(test_token)
        await asyncio.sleep(1)

        # 测试 4: 并发任务
        await self.test_concurrent_tasks()

        self.log(f"{Fore.GREEN + Style.BRIGHT}所有测试完成！{Style.RESET_ALL}")


async def main():
    """主函数"""
    demo = StorkTestDemo()
    await demo.run_all_tests()


if __name__ == "__main__":
    try:
        print(f"{Fore.CYAN}启动 Stork Bot 测试 Demo...{Style.RESET_ALL}\n")
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}用户中断测试{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}测试过程中发生错误: {e}{Style.RESET_ALL}")
