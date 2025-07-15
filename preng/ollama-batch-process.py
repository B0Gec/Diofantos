import asyncio
import json
import toml
import argparse
import random
import time
from datetime import datetime
from ollama import AsyncClient
from pathlib import Path

def log_message(message):
    """Prints a message with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}, {message}", flush=True)

def save_response(prompt, task_id, response_text, output_dir):
    """Saves the response to a JSON file with a unique filename."""
    # Generate a unique filename using the current epoch time and a random element
    epoch = int(time.time())
    random_suffix = random.randint(1000, 9999)
    filename = f"{task_id:0>5}-{random_suffix}.json"

    # Create the output dictionary
    output_data = {
        "prompt": prompt,
        "response": response_text
    }

    # Ensure the output directory exists
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write the response to the JSON file
    file_path = output_dir / filename
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)
        json_file.flush()

    #log_message(f"Response saved to {file_path}")
    
# The recommended parameters for precision and automation
OLLAMA_OPTIONS = {
    "temperature": 0.0,
    "top_p": 0.1,
    # "stop": ["```"], # Stop generation right after the code block
    # "num_predict": 512,
}

async def chat(system_msg, message, task_id, host, gpu_index, model, output_dir):
    try:
        # Start timing
        start_time = datetime.now()

        # Make the API request using the specified host and model
        response = await AsyncClient(host=f"http://{host}").chat(
            model=model,
            messages=[system_msg, message],
            options=OLLAMA_OPTIONS,
            stream=False
        )

        # Stop timing
        end_time = datetime.now()

        # Extract the response content
        response_text = response['message']['content']
        prompt_text = message['content']

        # Save the response to a JSON file
        save_response(prompt_text, task_id, response_text, output_dir)

        # Calculate duration and word count
        duration = (end_time - start_time).total_seconds()
        word_count = len(response_text.split())

        # Calculate words per second (WPS)
        wps = word_count / duration if duration > 0 else 0

        # Log the GPU index, word count, duration, and words per second
        log_message(f"Host: {host}, GPU: {gpu_index}, Words: {word_count}, Duration: {duration:.2f}s, WPS: {wps:.2f}")

    except Exception as e:
        log_message(f"Error on host {host}: {e}")

async def worker(host, gpu_index, model, task_queue, output_dir):
    """Worker function to process tasks using the specified host."""
    while not task_queue.empty():
        system_msg, message, task_id = await task_queue.get()
        # task_id = 2
        # print(task_id)
        await chat(system_msg, message, task_id, host, gpu_index, model, output_dir)
        task_queue.task_done()

async def main(config_path, prompts_path, output_dir, index_skip):
    # Get configuration  
    config = toml.load(config_path)
    model = config.get("model", "fakellama3.2force-error")
    gpus = config["ollama_instances"]
    system_msg = json.loads(f'{{"role": "system", "content": {json.dumps(config.get("system_message"))}}}')

    # Load prompts from JSONL file
    prompts = []
    with open(prompts_path, "r") as file:
        for line in file:
            prompts.append(json.loads(line))

    # Create an async queue and populate it with prompts
    task_queue = asyncio.Queue()
    for n, message in enumerate(prompts):
        # print(n)
        task_queue.put_nowait([system_msg, message, index_skip + n])

    # Create a list of worker tasks, one for each Ollama instance 
    tasks = []
    for host, gpu_index in gpus.items():
        tasks.append(worker(host, gpu_index, model, task_queue, output_dir))

    # Await the completion of all worker tasks
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ollama Batch Processing Client")
    parser.add_argument("--config", type=str, default="config.toml", help="Path to the configuration TOML file")
    parser.add_argument("--prompts", type=str, required=True, help="Path to the JSONL file with prompts")
    parser.add_argument("--output_dir", type=str, default="responses", help="Directory to save the response JSON files")
    # If doing cores in batches of 30 seqs, second batch will start with task_id = 00000 instead of 00030:
    parser.add_argument("--index_skip", type=int, default=0, help="keep task_id consistent with data set")

    args = parser.parse_args()

    try:
        asyncio.run(main(args.config, args.prompts, args.output_dir, args.index_skip))
        log_message("All prompts processed. Exiting...")
    except KeyboardInterrupt:
        log_message("Process interrupted by user. Exiting...")

