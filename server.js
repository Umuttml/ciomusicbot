require("dotenv").config();

const express=require("express");
const cors=require("cors");
const helmet=require("helmet");
const compression=require("compression");

const musicRoutes=require("./routes/music.routes");

const errorMiddleware=require("./middlewares/error.middleware");

const app=express();

app.use(cors());

app.use(helmet());

app.use(compression());

app.use(express.json());

app.get("/",(req,res)=>{

    res.json({

        success:true,

        app:"Cio Müzik API",

        version:"1.0.0"

    });

});

app.use("/api/music",musicRoutes);

app.use(errorMiddleware);

const PORT=process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`API çalışıyor: ${PORT}`);
});