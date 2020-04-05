If you have any implementation related issues, look at the README of actual repo.

**Stepwise saliency map generation**:
1. First unzip the folder 'pretrained_models', pull all the folders inside the folder 'models' into the folder 'visualize_atari'
2. Setup virtual environment and download the following dependencies(as per original repo)
            
        NumPy
        SciPy
        Matplotlib
        PyTorch 0.4.1
        Jupyter
    
3. Run 'script.txt'
          
          The script generates two movies, one with our metric and other with Greydanus'  

          In the script, for example in the following command,

          python3 make_movie.py --prefix atari --checkpoint strong.40.tar --first_frame 200 --env SpaceInvaders-v0

          You can change the first_frame of your choice to make the movie from there onwards. You can add flag --num_frames (Default 200) to increase or decrease the length of the movie.

4. Results are stored in the folder 'movies'
