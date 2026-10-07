from streamlit.testing.v1 import AppTest
import time

def run_tests():
    print("Initializing AppTest...")
    at = AppTest.from_file("app.py", default_timeout=30)
    
    print("Running app (Home)...")
    at.run()
    assert not at.exception, f"Exception on Home: {at.exception[0].message}"
    
    if len(at.radio) > 0:
        radio = at.radio[0]
        options = radio.options
        for opt in options:
            print(f"Testing page: {opt.encode('utf-8', 'ignore').decode('utf-8')}")
            radio.set_value(opt)
            at.run()
            if at.exception:
                print(f"EXCEPTION ON {opt.encode('utf-8', 'ignore').decode('utf-8')}: {at.exception[0].message}")
                assert False, f"Exception on {opt.encode('utf-8', 'ignore').decode('utf-8')}"
            print(f"  -> {opt.encode('utf-8', 'ignore').decode('utf-8')} loaded successfully.")
            
    print("All pages loaded successfully without exceptions!")

if __name__ == "__main__":
    run_tests()
