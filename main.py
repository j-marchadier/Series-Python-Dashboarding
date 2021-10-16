import data
import dashboard

if __name__ == "__main__":
    data_done = data.main()
    dashboard.main(data_done)
