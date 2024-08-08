"""
Executes task in the background and pings provided endpoint/url when done
"""
import concurrent.futures
from typing import Callable, Any
executor = concurrent.futures.ThreadPoolExecutor(max_workers=16)

def exec(f: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    return executor.submit(f, *args, **kwargs)
